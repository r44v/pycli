import click
import time
import pathlib
import os


@click.command()
@click.argument("reason")
@click.argument("seconds", type=int)
@click.option("--box", is_flag=True, help="Show a message box when the timer is done")
def timer(reason: str, seconds: int, box: bool):
    """Start a timer for a given amount of seconds and beep when the time is done"""

    print(f"Starting timer for {seconds} seconds because {reason}")

    total_seconds = seconds

    print()
    for seconds in range(1, total_seconds + 1):
        time.sleep(1)
        terminal_width = os.get_terminal_size().columns
        MAX_LEN = int(terminal_width * 2 / 3)
        completion = int((seconds / total_seconds) * MAX_LEN)
        completion_inverse = MAX_LEN - completion
        progress = (
            "["
            + "#" * completion
            + " " * completion_inverse
            + "]"
            + f" {seconds}/{total_seconds} seconds"
        )
        print(
            "\r" + progress + " " * (terminal_width - len(progress)), end="", flush=True
        )

    wav_path = pathlib.Path(__file__).parent / "timer.wav"

    # detect windows
    if os.name == "nt":
        import winsound

        winsound.PlaySound(wav_path.as_posix(), winsound.SND_FILENAME)

    print("\n\nDone!")

    if box:
        import tkinter as tk

        print("\nplease close the messagebox...")

        root = tk.Tk()

        root.title("Timer Done")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_height = 250
        window_width = 550

        geometry = "%dx%d+%d+%d" % (
            window_width,
            window_height,
            screen_width / 2 - (window_width // 2),
            screen_height / 2 - (window_height // 2),
        )
        print(geometry)
        root.geometry(geometry)
        text_box = tk.Text(root)
        text_box.insert(tk.END, reason)
        root.configure(background="red")
        root.lift()

        # TODO: cleanup

        # text_box = tk.Text(root)
        # text_box.insert(tk.END, reason)
        # root.attributes("-topmost", True)
        # root.after_idle(root.attributes, "-topmost", False)
        root.mainloop()

        # ctypes.windll.user32.MessageBoxW(0, reason, "Timer done", 0)
