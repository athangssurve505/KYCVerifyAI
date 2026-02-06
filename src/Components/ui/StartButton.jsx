export default function StartButton({ onStart ,disabled }) {
  return (
    <button
      onClick={onStart}
      disabled={disabled}
      className="mt-4 px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition cursor-pointer disabled:bg-blue-300 disabled:cursor-not-allowed"
    >
      Start Verification
    </button>
  );
}
