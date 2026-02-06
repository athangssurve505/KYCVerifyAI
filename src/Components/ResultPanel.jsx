export default function ResultPanel() {
  return (
    <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4 max-w-3xl mx-auto">

      <div className="bg-green-100 p-4 rounded-lg shadow">
        <p>✅ Real Person Detected</p>
        <p>✅ No Deepfake Found</p>
        <p>✅ Face Matched with Database</p>
        <p className="font-semibold mt-2">Confidence: 91%</p>
      </div>

      <div className="bg-red-100 p-4 rounded-lg shadow">
        <p>❌ Possible Deepfake</p>
        <p>❌ Face Not Matched</p>
        <p>Please Retry.</p>
      </div>

    </div>
  );
}
