import { useState } from "react";
import Prompt from "../Components/Instructions/Prompt";
import Loader from "../Components/Loader";
import ResultPanel from "../Components/ResultPanel";
import WebcamView from "../Components/WebCam";
import StartButton from "../Components/ui/StartButton";
import RetryButton from "../Components/ui/RetryButton";

export default function VerifyPage() {
  const [showCamera, setShowCamera] = useState(false);
  const [videoBlob, setVideoBlob] = useState(null);

  // This function will receive the recorded video
  const handleVideoRecorded = (blob) => {
    setVideoBlob(blob);

  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 text-center">
      <h1 className="text-2xl md:text-3xl font-semibold mb-6 bg-blue-600 p-2 text-white">
        AI-Powered KYC Verification
      </h1>

      {/* Show webcam and enable recording only after Start is clicked */}
      {showCamera ? (
        <WebcamView
          showText={false}
          onVideoRecorded={handleVideoRecorded}
        />
      ) : (
        <WebcamView showText={true} />
      )}

    <div className="flex gap-4 justify-around">
      <StartButton onStart={() => setShowCamera(true) } disabled={showCamera} />
        {/* 👉 NEW STOP BUTTON */}
    
        <button
  disabled={!showCamera}
  onClick={() => setShowCamera(false)}
  className="mt-3 px-6 py-2 bg-yellow-600 text-white rounded-lg cursor-pointer hover:bg-yellow-700 disabled:bg-yellow-400 disabled:cursor-not-allowed"
>
  Stop Verification
</button>

    
      </div>

      <Prompt />

      {/* You can enable loader later while processing */}
      {/* <Loader /> */}

      <ResultPanel />

      <RetryButton />

      {/* Optional: show recorded video preview */}
      {videoBlob && (
        <div className="mt-6">
          <p className="text-green-600 font-medium">
            ✅ Video recorded successfully!
          </p>

          <video
            src={URL.createObjectURL(videoBlob)}
            controls
            className="mt-4 mx-auto w-96 rounded-lg shadow"
          />
        </div>
      )}
    </div>
  );
}
