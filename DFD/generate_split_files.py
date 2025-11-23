import os
import random

dataset_root = 'Celeb-DF-v2'
real_dir = os.path.join(dataset_root, 'real')
fake_dir = os.path.join(dataset_root, 'fake')

real_videos = [os.path.join('real', f) for f in os.listdir(real_dir) if f.endswith('.mp4')]
fake_videos = [os.path.join('fake', f) for f in os.listdir(fake_dir) if f.endswith('.mp4')]

real_samples = [(path, 1) for path in real_videos]
fake_samples = [(path, 0) for path in fake_videos]

all_samples = real_samples + fake_samples
random.shuffle(all_samples)

# 80% train, 20% validation split
split_idx = int(0.8 * len(all_samples))
train_samples = all_samples[:split_idx]
val_samples = all_samples[split_idx:]

def write_split(samples, filename):
    with open(filename, 'w') as f:
        for path, label in samples:
            f.write(f"{path} {label}\n")

write_split(train_samples, 'train.txt')
write_split(val_samples, 'val.txt')

print(f"Generated train.txt and val.txt with {len(train_samples)} train and {len(val_samples)} val samples.")
