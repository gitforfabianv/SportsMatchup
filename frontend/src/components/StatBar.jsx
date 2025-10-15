export function StatBar({ value, max, color = "bg-blue-500", reverse = false, }) {
    const percentage = Math.min((value / max) * 100, 100);
    return (<div className={`w-full h-2 bg-gray-700 rounded overflow-hidden flex ${reverse ? "flex-row-reverse" : ""}`}>
      <div className={`h-full ${color}`} style={{ width: `${percentage}%` }}/>
    </div>);
}
