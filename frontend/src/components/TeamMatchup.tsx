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
  headToHeadTeam1Stats: Record<string, number | string>;
  headToHeadTeam2Stats: Record<string, number | string>;
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
  headToHeadTeam1Stats,
  headToHeadTeam2Stats,
  historicalTeam1Stats,
  historicalTeam2Stats,
  team1Accolades,
  team2Accolades,
}: TeamMatchupProps) {
  // 🧩 Define the desired display order
  const orderedStats = [
    { label: "PPG", key: "pts" },
    { label: "APG", key: "ast" },
    { label: "RPG", key: "trb" },
    { label: "3PG", key: "fg3" },
    { label: "SPG", key: "stl" },
    { label: "BPG", key: "blk" },
    { label: "TPG", key: "tov" },
  ];

  // 🧠 Identify the remaining stats not listed above
  const advancedStatKeys = Object.keys(headToHeadTeam1Stats).filter(
    (key) => !orderedStats.find((s) => s.key === key)
  );

  return (
    <div className="flex flex-col justify-center items-center space-y-6 bg-black text-white">
      {/* Logo */}
      <img
        src={MatchupsLogo}
        alt="Logo"
        width={70}
        height={70}
        draggable={false}
        className="cursor-pointer m-2"
      />

      {/* Teams Display */}
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

      {/* 📊 Primary Stats Section */}
      <div id="headtohead" className="w-full space-y-4">
        {orderedStats.map(({ label, key }) => {
          const team1Value =
            parseFloat(headToHeadTeam1Stats[key] as string) || 0;
          const team2Value =
            parseFloat(headToHeadTeam2Stats[key] as string) || 0;
          const max = Math.max(team1Value, team2Value, 1);

          return (
            <div key={key} className="w-full space-y-1">
              <div className="flex justify-between items-center text-xl text-center">
                <div className="text-right text-amber-300 w-1/3">
                  {team1Value.toFixed(1)}
                </div>
                <div className="w-1/3 font-semibold text-2xl">{label}</div>
                <div className="text-left text-amber-300 w-1/3">
                  {team2Value.toFixed(1)}
                </div>
              </div>

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

      {/* ⚙️ Advanced Stats Section */}
      {advancedStatKeys.length > 0 && (
        <div className="w-full mt-8 border-t border-gray-700 pt-4">
          <h3 className="text-center text-lg font-semibold mb-2 text-gray-300">
            Advanced Stats
          </h3>
          <div className="space-y-3">
            {advancedStatKeys.map((key) => {
              const team1Value =
                parseFloat(headToHeadTeam1Stats[key] as string) || 0;
              const team2Value =
                parseFloat(headToHeadTeam2Stats[key] as string) || 0;
              const max = Math.max(team1Value, team2Value, 1);

              return (
                <div key={key} className="w-full space-y-1">
                  <div className="flex justify-between items-center text-lg text-center">
                    <div className="text-right text-gray-400 w-1/3">
                      {team1Value.toFixed(1)}
                    </div>
                    <div className="w-1/3 font-semibold uppercase text-gray-300">
                      {key}
                    </div>
                    <div className="text-left text-gray-400 w-1/3">
                      {team2Value.toFixed(1)}
                    </div>
                  </div>

                  <div className="flex justify-center items-center gap-8">
                    <div className="w-1/3">
                      <StatBar
                        value={team1Value}
                        max={max}
                        color="bg-green-400"
                      />
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
        </div>
      )}

      {/* 🏆 Accolades */}
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
