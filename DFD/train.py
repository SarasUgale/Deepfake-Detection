import torch
from torch.utils.data import DataLoader
from model import Model
from dataset import CustomDataset  # Ensure this is correctly implemented
import torch.nn as nn
import torch.optim as optim
import os

def train():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load datasets
    print("Loading datasets...")
    train_dataset = CustomDataset('train.txt')
    val_dataset = CustomDataset('val.txt')

    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False, num_workers=0)

    # Initialize model
    model = Model(num_classes=2)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    # Training loop
    for epoch in range(10):
        print(f"\nEpoch {epoch+1}/10")
        model.train()
        running_loss = 0.0

        for i, (clips, labels) in enumerate(train_loader):
            try:
                clips = clips.squeeze(1).to(device)
                labels = labels.to(device)

                _, outputs = model(clips)
                loss = criterion(outputs, labels)

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_loss += loss.item()

                if i % 5 == 0:
                    print(f"[Batch {i}] Loss: {loss.item():.4f}")
            except Exception as e:
                print(f"[ERROR] Skipping batch {i} due to error: {e}")
                continue

        avg_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch+1} Average Loss: {avg_loss:.4f}")

    # Save model
    os.makedirs("model", exist_ok=True)
    torch.save(model.state_dict(), "model/df_model.pt")
    print("Model saved to model/df_model.pt")

if __name__ == '__main__':
    train()
