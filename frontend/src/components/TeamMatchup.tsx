"use client";
import { StatBar } from "./StatBar";
import MatchupsLogo from "../assets/MatchupsLogo.svg";

interface TeamMatchupProps {
  team1: string;
  team2: string;
  team1Image: string;
  team2Image: string;
  record: string;
  statLabels: string[];
  headToHeadTeam1Stats: string[];
  headToHeadTeam2Stats: string[];
  historicalTeam1Stats: string[];
  historicalTeam2Stats: string[];
  team1Accolades: string[];
  team2Accolades: string[];
}

export function TeamMatchup({
  team1,
  team2,
  team1Image,
  team2Image,
  statLabels,
  headToHeadTeam1Stats,
  headToHeadTeam2Stats,
  historicalTeam1Stats,
  historicalTeam2Stats,
  team1Accolades,
  team2Accolades,
}: TeamMatchupProps) {
  return (
    <div className="flex flex-col justify-center items-center space-y-6 bg-black text-white">
      {/* Record */}
      {/**<h2 className="text-xl font-bold">{record}</h2>**/}
      <img
        src={MatchupsLogo}
        alt="Logo"
        width={70}
        height={70}
        draggable={false}
        className="cursor-pointer m-2"
      />

      {/* Team Images */}
      <div className="flex justify-center items-center w-full">
        <div className="w-1/3 flex flex-col justify-center items-center">
          <span className="text-3xl text-center my-2">{team1}</span>
          <img
            src={team1Image}
            alt="Team 1"
            className="h-20 w-20 object-contain"
          />
        </div>

        <div className="w-auto flex flex-col justify-center">
          <span className="text-4xl font-semibold">vs</span>
        </div>

        <div className="w-1/3 flex flex-col justify-center items-center">
          <span className="text-3xl text-center my-2">{team2}</span>
          <img
            src={team2Image}
            alt="Team 2"
            className="h-20 w-20 object-contain"
          />
        </div>
      </div>

      {/* Head-to-Head Stats */}
      <div id="headtohead" className="w-full space-y-4">
        {statLabels.map((label, i) => {
          const team1Value = parseFloat(headToHeadTeam1Stats[i]);
          const team2Value = parseFloat(headToHeadTeam2Stats[i]);
          const max = Math.max(team1Value, team2Value);

          return (
            <div key={i} className="w-full space-y-1">
              {/* Stat Values Row */}
              <div className="flex justify-between items-center text-xl text-center">
                <div className="text-right text-amber-300 w-1/3">
                  {team1Value}
                </div>
                <div className="w-1/3 font-semibold text-2xl">{label}</div>
                <div className="text-left text-amber-300 w-1/3">
                  {team2Value}
                </div>
              </div>

              {/* StatBar Row */}
              <div className="flex justify-center items-center gap-8">
                <div className="w-1/3">
                  <StatBar value={team1Value} max={max} color="bg-green-400" />
                </div>
                <div className="w-1/3">
                  <StatBar
                    value={team2Value}
                    max={max}
                    color="bg-red-400"
                    reverse
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Historical Stats */}
      <div className="w-full grid grid-cols-3 gap-4 text-center mt-6">
        <div className="space-y-2">
          {historicalTeam1Stats.map((stat, i) => (
            <div key={i}>{stat}</div>
          ))}
        </div>
        <div className="space-y-2 font-semibold">
          {statLabels.map((_, i) => (
            <div key={i}>Avg (All Time)</div>
          ))}
        </div>
        <div className="space-y-2">
          {historicalTeam2Stats.map((stat, i) => (
            <div key={i}>{stat}</div>
          ))}
        </div>
      </div>

      {/* Accolades */}
      <div className="w-full grid grid-cols-2 gap-8 mt-6 text-sm">
        <div className="space-y-1">
          <h3 className="font-semibold text-center">Team 1 Accolades</h3>
          {team1Accolades.map((item, i) => (
            <div key={i} className="text-center">
              {item}
            </div>
          ))}
        </div>
        <div className="space-y-1">
          <h3 className="font-semibold text-center">Team 2 Accolades</h3>
          {team2Accolades.map((item, i) => (
            <div key={i} className="text-center">
              {item}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
