import torch
import torch.nn as nn
import torchvision.models as models


class ViolenceDetectionModel(nn.Module):
    def __init__(self):
        super(ViolenceDetectionModel, self).__init__()
        # CNN (ResNet) as feature extractor
        resnet = models.resnet50(pretrained=True)
        self.feature_extractor = nn.Sequential(*list(resnet.children())[:-1])

        # LSTM for temporal feature extraction
        self.lstm = nn.LSTM(input_size=2048, hidden_size=128, num_layers=2, batch_first=True)
        self.fc = nn.Linear(128, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        batch_size, seq_len, c, h, w = x.shape
        x = x.view(batch_size * seq_len, c, h, w)

        with torch.no_grad():
            x = self.feature_extractor(x)

        x = x.view(batch_size, seq_len, -1)
        lstm_out, _ = self.lstm(x)
        output = self.sigmoid(self.fc(lstm_out[:, -1, :]))
        return output
