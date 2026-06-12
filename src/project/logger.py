"""
AUTHOR: Rohan Joseph
PURPOSE: Execution logging utilities for the AI occupation adoption-gap dashboard.
DATE CREATED: 2026-06-04
DATE MODIFIED: 2026-06-12
MODIFIED BY: Rohan Joseph
"""



"""
Importing Libraries and Utilities
"""

# --- Import standard libraries ---
import datetime
import os
import sys



"""
Classes
"""

class TeeStream:
    """
    Write to multiple streams at the same time.
    This preserves console visibility while also storing a Markdown run log.
    """

    def __init__(self, streams):
        """
        Store the underlying streams that should receive mirrored output.
        """

        self.streams = streams

    def write(self, data):
        """
        Forward text to every target stream and keep them flushed in step.
        """

        for stream in self.streams:
            try:
                stream.write(data)
            except Exception:
                pass
        self.flush()

    def flush(self):
        """
        Flush each underlying stream when it supports flushing.
        """

        for stream in self.streams:
            try:
                stream.flush()
            except Exception:
                pass



"""
Functions
"""

def capture_script_console_to_markdown(
    run_callable,
    output_dir: str,
    script_name: str,
    also_print_to_console: bool = True,
) -> str:
    """
    Capture stdout and stderr for a callable into a Markdown log file.
    This preserves reproducible execution transcripts for setup, checks, validation, and app launch.
    """

    os.makedirs(output_dir, exist_ok = True)
    markdown_path = os.path.join(output_dir, f"{script_name}.md")

    original_stdout = sys.stdout
    original_stderr = sys.stderr
    markdown_handle = None

    try:
        markdown_handle = open(markdown_path, "w", encoding = "utf-8")

        if also_print_to_console:
            sys.stdout = TeeStream([original_stdout, markdown_handle])
            sys.stderr = TeeStream([original_stderr, markdown_handle])
        else:
            sys.stdout = markdown_handle
            sys.stderr = markdown_handle

        start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print(f"# Script run log: {script_name}")
        print("")
        print(f"- **Start:** {start_time}")
        print("")
        print("```text")

        run_callable()

        print("```")
        print("")
        print(f"- **End:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception:
        try:
            print("```")
        except Exception:
            pass
        raise

    finally:
        sys.stdout = original_stdout
        sys.stderr = original_stderr

        if markdown_handle is not None:
            markdown_handle.close()

    return markdown_path
