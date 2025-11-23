import torch
from torch.utils.data import Dataset
import cv2
import numpy as np
from torchvision import transforms

class CustomDataset(Dataset):
    def __init__(self, txt_file, sequence_length=20, transform=None):
        self.sequence_length = sequence_length
        self.transform = transform if transform else transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((112, 112)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
        
        self.data = []
        with open(txt_file, 'r') as file:
            for line in file:
                path, label = line.strip().split()
                self.data.append((path, int(label)))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        video_path, label = self.data[idx]
        frames = self.extract_frames(video_path)

        if len(frames) == 0:
            # Return dummy tensor if frame extraction fails
            dummy_frame = torch.zeros(3, 112, 112)
            frames = [dummy_frame for _ in range(self.sequence_length)]
        else:
            # Pad if frames are less than required
            while len(frames) < self.sequence_length:
                frames.append(torch.zeros_like(frames[0]))

        frames = torch.stack(frames[:self.sequence_length])
        return frames.unsqueeze(0), torch.tensor(label)

    def extract_frames(self, path):
        cap = cv2.VideoCapture(path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if not cap.isOpened() or total_frames < 1:
            return []

        frames = []
        step = max(1, total_frames // self.sequence_length)
        for i in range(self.sequence_length):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i * step)
            success, frame = cap.read()
            if success:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = self.transform(frame)
                frames.append(frame)
        cap.release()
        return frames
