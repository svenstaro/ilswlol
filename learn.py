from datetime import datetime
import pandas as pd
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

lukas_frame = pd.read_csv('lukas.csv')

dtype = torch.FloatTensor
if torch.cuda.is_available():
    print("CUDA available, running on GPU")
    dtype = torch.cuda.DoubleTensor

input_tensor = torch.from_numpy(lukas_frame[["timestamp", "awakeness_confidence"]].values)
timestamps = Variable(input_tensor).type(dtype)[:, :1]
timestamps = timestamps.unsqueeze(1)
time_of_day = Variable(dtype([(datetime.fromtimestamp(x) - datetime.fromtimestamp(x).replace(hour=0, minute=0, second=0, microsecond=0)).seconds / 86400 for x in timestamps]))
print(time_of_day)
time_of_day = time_of_day.unsqueeze(1).unsqueeze(1)
# time_of_day = Variable(torch.randn(1000, 1, 1).type(dtype))
target_confidences = Variable(input_tensor).type(dtype)[:, 1:2]


class LukasLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(LukasLSTM, self).__init__()
        self.hidden_dim = hidden_dim

        self.lstm = nn.LSTM(input_dim, self.hidden_dim).type(dtype)
        self.lstm.cuda()

        # Linear layer to map from hidden state space to confidence space.
        self.hidden_to_confidence = nn.Linear(self.hidden_dim, 1).type(dtype)
        self.init_hidden()

    def init_hidden(self):
        # Initialize hidden state.
        self.hidden = (Variable(torch.randn(1, 1, self.hidden_dim).type(dtype)),
                       Variable(torch.randn(1, 1, self.hidden_dim).type(dtype)))

    def forward(self, inputs):
        lstm_output, self.hidden = self.lstm(inputs, self.hidden)
        final_output = self.hidden_to_confidence(lstm_output)
        return final_output


hidden_dim = 24  # Maybe it can find 24h patterns?
lukas_model = LukasLSTM(1, hidden_dim).cuda()
criterion = nn.MSELoss()
criterion.cuda()
optimizer = optim.LBFGS(lukas_model.parameters(), lr=0.05)

for epoch in range(15):
    print(f"Step {epoch}")

    def closure():
        lukas_model.zero_grad()

        lukas_model.init_hidden()

        confidences = lukas_model(time_of_day)

        loss = criterion(confidences, target_confidences)
        print(f'loss: {loss.data.cpu().numpy()[0]}')
        loss.backward()
        return loss
    optimizer.step(closure)

# Draw the result.
plt.figure(figsize=(30, 10))
plt.title('Predict future values for time sequences\n(Dashlines are predicted values)',
          fontsize=30)
plt.xlabel('timestamps', fontsize=20)
plt.ylabel('awakeness_confidence', fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
# Show last 1000 values in training set and predicted 1000 values.
known_x = list(map(datetime.fromtimestamp, timestamps.data.cpu().numpy()))
known_y = target_confidences.data.cpu().numpy()

# Get the delta between two datetimes
delta = known_x[-1] - known_x[-2]
# Generate more future dates to predict
future = 1000
extrapolated_x = [known_x[-1] + delta]
for i in range(future - 1):
    extrapolated_x.append(extrapolated_x[-1] + delta)
extrapolated_x_variable = Variable(dtype([x.timestamp() for x in extrapolated_x]))
# Predict the future!
predicted_confidences = lukas_model(extrapolated_x_variable.unsqueeze(1).unsqueeze(1))
print(predicted_confidences)
plt.plot_date(known_x, known_y, linewidth=2.0, fmt="b-")
plt.plot_date(extrapolated_x, predicted_confidences.view(-1).data.cpu().numpy(), linewidth=2.0, fmt="r:")
plt.xticks(rotation=25)
plt.savefig("graph.png")
