import { useState } from "react";
import { TeamSelect } from "../sub/team-select";
import { TeamMatchup } from "../sub/TeamMatchup";

export const Versus = () => {
  const [teamA, setTeamA] = useState("");
  const [teamB, setTeamB] = useState("");
  const [submitted, setSubmitted] = useState(false);

const teams2 = [
  { id: "ATL", name: "Atlanta Hawks", image: "https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg" },
  { id: "BOS", name: "Boston Celtics", image: "https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg" },
  { id: "BKN", name: "Brooklyn Nets", image: "https://upload.wikimedia.org/wikipedia/en/4/40/Brooklyn_Nets_primary_icon_logo_2024.svg" },
  { id: "CHA", name: "Charlotte Hornets", image: "https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg" },
  { id: "CHI", name: "Chicago Bulls", image: "https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg" },
  { id: "CLE", name: "Cleveland Cavaliers", image: "https://upload.wikimedia.org/wikipedia/commons/4/4b/Cleveland_Cavaliers_logo.svg" },
  { id: "DAL", name: "Dallas Mavericks", image: "https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg" },
  { id: "DEN", name: "Denver Nuggets", image: "https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg" },
  { id: "DET", name: "Detroit Pistons", image: "https://upload.wikimedia.org/wikipedia/commons/c/c9/Logo_of_the_Detroit_Pistons.svg" },
  { id: "GSW", name: "Golden State Warriors", image: "https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg" },
  { id: "HOU", name: "Houston Rockets", image: "https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg" },
  { id: "IND", name: "Indiana Pacers", image: "https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg" },
  { id: "LAC", name: "Los Angeles Clippers", image: "https://upload.wikimedia.org/wikipedia/en/e/ed/Los_Angeles_Clippers_%282024%29.svg" },
  { id: "LAL", name: "Los Angeles Lakers", image: "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg" },
  { id: "MEM", name: "Memphis Grizzlies", image: "https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg" },
  { id: "MIA", name: "Miami Heat", image: "https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg" },
  { id: "MIL", name: "Milwaukee Bucks", image: "https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg" },
  { id: "MIN", name: "Minnesota Timberwolves", image: "https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg" },
  { id: "NOP", name: "New Orleans Pelicans", image: "https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg" },
  { id: "NYK", name: "New York Knicks", image: "https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg" },
  { id: "OKC", name: "Oklahoma City Thunder", image: "https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg" },
  { id: "ORL", name: "Orlando Magic", image: "https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg" },
  { id: "PHI", name: "Philadelphia 76ers", image: "https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg" },
  { id: "PHX", name: "Phoenix Suns", image: "https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg" },
  { id: "POR", name: "Portland Trail Blazers", image: "https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg" },
  { id: "SAC", name: "Sacramento Kings", image: "https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg" },
  { id: "SAS", name: "San Antonio Spurs", image: "https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg" },
  { id: "TOR", name: "Toronto Raptors", image: "https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg" },
  { id: "UTA", name: "Utah Jazz", image: "https://upload.wikimedia.org/wikipedia/en/7/77/Utah_Jazz_logo_2025.svg" },
  { id: "WAS", name: "Washington Wizards", image: "https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg" },
];

  const handleSubmit = () => {
    if (teamA && teamB) {
      console.log("Submitted:", teamA, "vs", teamB);
      setSubmitted(true);
    }
  };

  return (
    <div
    className="w-full h-full flex flex-col justify-center items-center"
    style={{ backgroundImage: `url("")`, backgroundSize: 'cover', backgroundPosition: 'center' }}
  >
    <div className="flex flex-row justify-evenly items-center w-full h-64">
      <div className="w-[20%] h-[60%] bg-transparent border border-gray-300">
        <TeamSelect
          label="Team A"
          value={teamA}
          onChange={setTeamA}
          options={teams2}
        />
      </div>

        <div className="flex flex-col justify-center items-center text-gray-800">
        <h2 className="text-center text-lg">VS</h2>
        <button
          onClick={handleSubmit}
          disabled={!teamA || !teamB}
          className={`px-6 py-2 rounded-lg font-semibold transition ${
            teamA && teamB
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          Submit
        </button>
      </div>

      <div className="w-[20%] h-[60%] bg-transparent border border-gray-300">
        <TeamSelect
          label="Team B"
          value={teamB}
          onChange={setTeamB}
          options={teams2}
        />
      </div>
    </div>

      {submitted && (
        <div className="w-full flex justify-center">
          <div className="w-full max-w-4xl bg-white border border-gray-300 rounded-lg shadow p-6">
            <TeamMatchup
              team1Image={teams2.find((team) => team.id === teamA)?.image || "/images/default.png"}
              team2Image={teams2.find((team) => team.id === teamB)?.image || "/images/default.png"}
              team1Name={teams2.find((team) => team.id === teamA)?.name || "Team A"}
              team2Name={teams2.find((team) => team.id === teamB)?.name || "Team B"}
              record={`${teams2.find((team) => team.id === teamA)?.name || "Team A"} vs ${teams2.find((team) => team.id === teamB)?.name || "Team B"}`}
              statLabels={["PPG", "RPG", "APG", "3P%"]}
              headToHeadTeam1Stats={["101.4", "45.2", "24.1", "36.1%"]}
              headToHeadTeam2Stats={["98.7", "43.5", "22.8", "38.6%"]}
              historicalTeam1Stats={["99.8", "44.9", "23.5", "35.4%"]}
              historicalTeam2Stats={["100.2", "46.1", "25.0", "37.0%"]}
              team1Accolades={["🏆 3× Champs", "⭐ 5× All-Stars"]}
              team2Accolades={["🏆 1× Champion", "⭐ 4× All-Stars"]}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default Versus;