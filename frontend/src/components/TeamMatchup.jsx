"use client";
import { StatBar } from "./StatBar";
export function TeamMatchup({ team1Image, team2Image, record, statLabels, headToHeadTeam1Stats, headToHeadTeam2Stats, historicalTeam1Stats, historicalTeam2Stats, team1Accolades, team2Accolades, }) {
    return (<div className="flex flex-col justify-center items-center space-y-6 bg-black text-white">
      {/* Record */}
      <h2 className="text-xl font-bold">{record}</h2>

      {/* Team Images */}
      <div className="flex justify-around items-center w-full">
        <img src={team1Image} alt="Team 1" className="h-20 w-20 object-contain"/>
        <span className="text-lg font-semibold">vs</span>
        <img src={team2Image} alt="Team 2" className="h-20 w-20 object-contain"/>
      </div>

      {/* Head-to-Head Stats */}
      <div className="w-full grid grid-cols-3 gap-4 text-center">
        <div className="space-y-2">
          {headToHeadTeam1Stats.map((stat, i) => {
            const value = parseFloat(stat);
            const opponentValue = parseFloat(headToHeadTeam2Stats[i]);
            const max = Math.max(value, opponentValue);
            return (<div key={i} className="space-y-1">
                <div>{stat}</div>
                <StatBar value={value} max={max} color="bg-red-500"/>
              </div>);
        })}
        </div>
        <div className="space-y-2 font-semibold">
          {statLabels.map((label, i) => (<div key={i}>{label}</div>))}
        </div>
        <div className="space-y-2">
          {headToHeadTeam2Stats.map((stat, i) => {
            const value = parseFloat(stat);
            const opponentValue = parseFloat(headToHeadTeam1Stats[i]);
            const max = Math.max(value, opponentValue);
            return (<div key={i} className="space-y-1">
                <div>{stat}</div>
                <StatBar value={value} max={max} color="bg-green-500" reverse/>
              </div>);
        })}
        </div>
      </div>

      {/* Historical Stats */}
      <div className="w-full grid grid-cols-3 gap-4 text-center mt-6">
        <div className="space-y-2">
          {historicalTeam1Stats.map((stat, i) => (<div key={i}>{stat}</div>))}
        </div>
        <div className="space-y-2 font-semibold">
          {statLabels.map((_, i) => (<div key={i}>Avg (All Time)</div>))}
        </div>
        <div className="space-y-2">
          {historicalTeam2Stats.map((stat, i) => (<div key={i}>{stat}</div>))}
        </div>
      </div>

      {/* Accolades */}
      <div className="w-full grid grid-cols-2 gap-8 mt-6 text-sm">
        <div className="space-y-1">
          <h3 className="font-semibold text-center">Team 1 Accolades</h3>
          {team1Accolades.map((item, i) => (<div key={i} className="text-center">
              {item}
            </div>))}
        </div>
        <div className="space-y-1">
          <h3 className="font-semibold text-center">Team 2 Accolades</h3>
          {team2Accolades.map((item, i) => (<div key={i} className="text-center">
              {item}
            </div>))}
        </div>
      </div>
    </div>);
}
