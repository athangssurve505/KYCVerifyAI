import { useRef, useState } from "react";
import Webcam from "react-webcam";

export default function WebcamView({ showText, onVideoRecorded }) {
  const webcamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const recordedChunks = useRef([]);

  const [recording, setRecording] = useState(false);

  const startRecording = () => {
    recordedChunks.current = [];

    const stream = webcamRef.current.stream;
    mediaRecorderRef.current = new MediaRecorder(stream, {
      mimeType: "video/webm",
    });

    mediaRecorderRef.current.ondataavailable = (event) => {
      if (event.data.size > 0) {
        recordedChunks.current.push(event.data);
      }
    };

    mediaRecorderRef.current.onstop = () => {
      const videoBlob = new Blob(recordedChunks.current, {
        type: "video/webm",
      });

      // send video back to VerifyPage
      onVideoRecorded(videoBlob);
    };

    mediaRecorderRef.current.start();
    setRecording(true);

    // auto stop after 3 seconds
    setTimeout(() => {
      mediaRecorderRef.current.stop();
      setRecording(false);
    }, 3000);
  };

  return (
    <div className="relative w-full max-w-3xl h-80 mx-auto bg-gray-200 rounded-xl flex items-center justify-center shadow-md overflow-hidden">

      {showText ? (
        <p className="text-gray-600">📷 Live Camera Feed Here</p>
      ) : (
        <>
          <Webcam
            ref={webcamRef}
            audio={false}
            className="w-full h-full object-contain"
          />

          <button
            onClick={startRecording}
            disabled={recording}
            className={`absolute bottom-4 left-1/2 -translate-x-1/2 px-5 py-2 rounded-lg text-white font-medium ${
              recording ? "bg-gray-500" : "bg-red-600 hover:bg-red-700"
            }`}
          >
            {recording ? "Recording..." : "Start Recording (3s)"}
          </button>
        </>
      )}
    </div>
  );
}
