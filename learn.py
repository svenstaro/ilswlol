from datetime import datetime
import pandas as pd
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

torch.manual_seed(1)

lukas_frame = pd.read_csv('lukas.csv')

input_tensor = torch.from_numpy(lukas_frame[["timestamp", "awakeness_confidence"]].values)
timestamps = Variable(input_tensor).float()[:, :1]
target_confidences = Variable(input_tensor).float()[:, 1:2]


class LukasLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(LukasLSTM, self).__init__()
        self.hidden_dim = hidden_dim

        self.lstm = nn.LSTM(input_dim, self.hidden_dim)

        # Linear layer to map from hidden state space to confidence space.
        self.hidden_to_confidence = nn.Linear(self.hidden_dim, 1)
        self.init_hidden()

    def init_hidden(self):
        # Initialize hidden state.
        self.hidden = (Variable(torch.zeros(1, 1, self.hidden_dim)),
                       Variable(torch.zeros(1, 1, self.hidden_dim)))

    def forward(self, inputs):
        output, self.hidden = self.lstm(inputs, self.hidden)
        output = self.hidden_to_confidence(output)
        return output


hidden_dim = 24  # Maybe it can find 24h patterns?
lukas_model = LukasLSTM(1, hidden_dim)
loss = nn.MSELoss()
optimizer = optim.LBFGS(lukas_model.parameters(), lr=0.8)

confidences = lukas_model(timestamps)
print(confidences)

for epoch in range(15):
    print(f"Step {epoch}")

    def closure():
        lukas_model.zero_grad()

        lukas_model.hidden = lukas_model.init_hidden()

        confidences = lukas_model(timestamps)

        output = loss(confidences, target_confidences)
        output.backward()
        return output
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
known_x = list(map(datetime.fromtimestamp, timestamps[9000:].data.numpy()))
known_y = target_confidences[9000:].data.numpy()

# Get the delta between two datetimes
delta = known_x[-1] - known_x[-2]
# Generate more future dates to predict
future = 1000
extrapolated_x = [known_x[-1] + delta]
for i in range(future - 1):
    extrapolated_x.append(extrapolated_x[-1] + delta)
extrapolated_x_variable = Variable(torch.FloatTensor([x.timestamp() for x in extrapolated_x]))
# Predict the future!
predicted_confidences = lukas_model(extrapolated_x_variable.view(-1, 1))
print(confidences)
plt.plot_date(known_x, known_y, linewidth=2.0, fmt="b-")
plt.plot_date(extrapolated_x, predicted_confidences.view(-1).data.numpy(), linewidth=2.0, fmt="r:")
plt.xticks(rotation=25)
plt.show()
