import re

log_file = "logs/gateway.log"

total_messages = 0
local_count = 0
cloud_count = 0

with open(log_file, "r") as file:
    for line in file:

        total_messages += 1

        if "Route: LOCAL" in line:
            local_count += 1

        if "Route: CLOUD" in line:
            cloud_count += 1

print("\nGateway Evaluation Report")
print("--------------------------")

print("Total messages processed:", total_messages)
print("Messages routed locally:", local_count)
print("Messages routed to cloud:", cloud_count)

if total_messages > 0:
    local_percent = (local_count / total_messages) * 100
    cloud_percent = (cloud_count / total_messages) * 100

    print(f"Local processing percentage: {local_percent:.2f}%")
    print(f"Cloud processing percentage: {cloud_percent:.2f}%")
