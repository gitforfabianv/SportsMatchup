interface StatBarProps {
  value: number;
  max: number;
  color?: string;
  reverse?: boolean;
}

export function StatBar({
  value,
  max,
  color = "bg-yellow-400",
  reverse = false,
}: StatBarProps) {
  const totalBlocks = 20; // Number of pixel segments
  const filledBlocks = Math.round((value / max) * totalBlocks);

  const blocks = Array.from({ length: totalBlocks }, (_, i) => {
    const isFilled = reverse
      ? i >= totalBlocks - filledBlocks
      : i < filledBlocks;
    return (
      <div
        key={i}
        className={`w-1 h-4 mx-[1px] ${
          isFilled ? color : "bg-gray-800"
        } rounded-sm shadow-sm`}
      />
    );
  });

  return (
    <div className="flex justify-center items-center overflow-hidden">
      {blocks}
    </div>
  );
}
