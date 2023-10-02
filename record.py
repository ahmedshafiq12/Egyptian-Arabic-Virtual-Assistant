from Recorder.VideoRecorder import *

if __name__ == "__main__":
    filename = "Default_user"
    file_manager(filename)
    start_AVrecording(filename)
    time.sleep(50)
    stop_AVrecording(filename)
    print("Done")