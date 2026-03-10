from utils.controller import PulseGenerator

starting_v = 0.5
step_width = 0.5
max_v = 5.0
min_v = 0.0

stim = PulseGenerator()
current_v = starting_v
final_v = None


def send_shock(voltage):
    stim.pulse(voltage)
    print(f"Shock administered at {voltage:.2f} mA")


print("Shock calibration started.")
print()
print("Commands:")
print("  s / shock    -> send shock at current mA")
print("  i / increase -> increase by 0.5 mA, then send shock")
print("  d / decrease -> enter a custom lower current level, then send shock")
print("  f / finish   -> lock in current mA as final")
print("  q / quit     -> exit without saving a final value")
print()

while True:
    print(f"Current level: {current_v:.2f} mA")
    cmd = input("Enter command: ").strip().lower()

    if cmd in ["s", "shock"]:
        send_shock(current_v)
        first_shock_sent = True

    elif cmd in ["i", "increase"]:
        if not first_shock_sent:
            print("You must deliver the first shock at 0.50 mA before increasing.")
            continue

        proposed_v = current_v + step_width
        if proposed_v > max_v:
            print(f"Current cannot exceed {max_v:.2f} mA.")
            print("No shock administered.")
        else:
            current_v = proposed_v
            send_shock(current_v)

    elif cmd in ["d", "decrease"]:
        if not first_shock_sent:
            print("You must deliver the first shock at 0.50 mA before decreasing.")
            continue

        try:
            new_v = float(input("Enter new current level: ").strip())

            if new_v < min_v:
                print(f"Current cannot be below {min_v:.2f} mA.")
                print("No shock administered.")
            elif new_v > max_v:
                print(f"Current cannot exceed {max_v:.2f} mA.")
                print("No shock administered.")
            elif new_v >= current_v:
                print("Entered value must be lower than the current mA.")
                print("No shock administered.")
            else:
                current_v = new_v
                send_shock(current_v)

        except ValueError:
            print("Invalid input. Please enter a numeric current level")

    elif cmd in ["f", "final"]:
        if not first_shock_sent:
            print("You must deliver the first shock at 0.50 mA before locking in a final value.")
            continue

        final_v = current_v
        print(f"Final current level locked in at {final_v:.2f} mA")
        break

    elif cmd in ["q", "quit"]:
        print("Exited without locking in a final current level.")
        break

    else:
        print("Invalid command. Please try again.")

print()
if final_v is not None:
    print(f"Workup complete. Final current level: {final_v:.2f} mA")
    print("RECORD FINAL CURRENT LEVEL IN EXPERIMENTER DATABASE")
else:
    print("Workup ended with no final current level selected.")



