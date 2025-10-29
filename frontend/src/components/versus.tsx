import { useState, useEffect } from "react";
import { TeamMatchup } from "./TeamMatchup";
import { RevealBlock } from "./RevealBlock";
import { CustomSelect } from "./CustomSelect";

interface Team {
  id?: string;
  name: string;
  image: string;
  short_name?: string;
}

interface VersusProps {
  teams?: Team[];
}

interface HeadToHeadData {
  [key: string]: {
    [team: string]: Record<string, number | string>;
    games_count?: number;
  };
}

// Define the local fallback teams array
const localTeams: Team[] = [
  {
    id: "ATL",
    name: "Atlanta Hawks",
    image:
      "https://upload.wikimedia.org/wikipedia/en/2/24/Atlanta_Hawks_logo.svg",
  },
  {
    id: "BOS",
    name: "Boston Celtics",
    image: "https://upload.wikimedia.org/wikipedia/en/8/8f/Boston_Celtics.svg",
  },
  {
    id: "BKN",
    name: "Brooklyn Nets",
    image:
      "https://upload.wikimedia.org/wikipedia/en/4/40/Brooklyn_Nets_primary_icon_logo_2024.svg",
  },
  {
    id: "CHA",
    name: "Charlotte Hornets",
    image:
      "https://upload.wikimedia.org/wikipedia/en/c/c4/Charlotte_Hornets_%282014%29.svg",
  },
  {
    id: "CHI",
    name: "Chicago Bulls",
    image:
      "https://upload.wikimedia.org/wikipedia/en/6/67/Chicago_Bulls_logo.svg",
  },
  {
    id: "CLE",
    name: "Cleveland Cavaliers",
    image:
      "https://upload.wikimedia.org/wikipedia/commons/4/4b/Cleveland_Cavaliers_logo.svg",
  },
  {
    id: "DAL",
    name: "Dallas Mavericks",
    image:
      "https://upload.wikimedia.org/wikipedia/en/9/97/Dallas_Mavericks_logo.svg",
  },
  {
    id: "DEN",
    name: "Denver Nuggets",
    image: "https://upload.wikimedia.org/wikipedia/en/7/76/Denver_Nuggets.svg",
  },
  {
    id: "DET",
    name: "Detroit Pistons",
    image:
      "https://upload.wikimedia.org/wikipedia/commons/c/c9/Logo_of_the_Detroit_Pistons.svg",
  },
  {
    id: "GSW",
    name: "Golden State Warriors",
    image:
      "https://upload.wikimedia.org/wikipedia/en/0/01/Golden_State_Warriors_logo.svg",
  },
  {
    id: "HOU",
    name: "Houston Rockets",
    image: "https://upload.wikimedia.org/wikipedia/en/2/28/Houston_Rockets.svg",
  },
  {
    id: "IND",
    name: "Indiana Pacers",
    image: "https://upload.wikimedia.org/wikipedia/en/1/1b/Indiana_Pacers.svg",
  },
  {
    id: "LAC",
    name: "Los Angeles Clippers",
    image:
      "https://upload.wikimedia.org/wikipedia/en/e/ed/Los_Angeles_Clippers_%282024%29.svg",
  },
  {
    id: "LAL",
    name: "Los Angeles Lakers",
    image:
      "https://upload.wikimedia.org/wikipedia/commons/3/3c/Los_Angeles_Lakers_logo.svg",
  },
  {
    id: "MEM",
    name: "Memphis Grizzlies",
    image:
      "https://upload.wikimedia.org/wikipedia/en/f/f1/Memphis_Grizzlies.svg",
  },
  {
    id: "MIA",
    name: "Miami Heat",
    image: "https://upload.wikimedia.org/wikipedia/en/f/fb/Miami_Heat_logo.svg",
  },
  {
    id: "MIL",
    name: "Milwaukee Bucks",
    image:
      "https://upload.wikimedia.org/wikipedia/en/4/4a/Milwaukee_Bucks_logo.svg",
  },
  {
    id: "MIN",
    name: "Minnesota Timberwolves",
    image:
      "https://upload.wikimedia.org/wikipedia/en/c/c2/Minnesota_Timberwolves_logo.svg",
  },
  {
    id: "NOP",
    name: "New Orleans Pelicans",
    image:
      "https://upload.wikimedia.org/wikipedia/en/0/0d/New_Orleans_Pelicans_logo.svg",
  },
  {
    id: "NYK",
    name: "New York Knicks",
    image:
      "https://upload.wikimedia.org/wikipedia/en/2/25/New_York_Knicks_logo.svg",
  },
  {
    id: "OKC",
    name: "Oklahoma City Thunder",
    image:
      "https://upload.wikimedia.org/wikipedia/en/5/5d/Oklahoma_City_Thunder.svg",
  },
  {
    id: "ORL",
    name: "Orlando Magic",
    image:
      "https://upload.wikimedia.org/wikipedia/en/1/10/Orlando_Magic_logo.svg",
  },
  {
    id: "PHI",
    name: "Philadelphia 76ers",
    image:
      "https://upload.wikimedia.org/wikipedia/en/0/0e/Philadelphia_76ers_logo.svg",
  },
  {
    id: "PHX",
    name: "Phoenix Suns",
    image:
      "https://upload.wikimedia.org/wikipedia/en/d/dc/Phoenix_Suns_logo.svg",
  },
  {
    id: "POR",
    name: "Portland Trail Blazers",
    image:
      "https://upload.wikimedia.org/wikipedia/en/2/21/Portland_Trail_Blazers_logo.svg",
  },
  {
    id: "SAC",
    name: "Sacramento Kings",
    image: "https://upload.wikimedia.org/wikipedia/en/c/c7/SacramentoKings.svg",
  },
  {
    id: "SAS",
    name: "San Antonio Spurs",
    image:
      "https://upload.wikimedia.org/wikipedia/en/a/a2/San_Antonio_Spurs.svg",
  },
  {
    id: "TOR",
    name: "Toronto Raptors",
    image:
      "https://upload.wikimedia.org/wikipedia/en/3/36/Toronto_Raptors_logo.svg",
  },
  {
    id: "UTA",
    name: "Utah Jazz",
    image:
      "https://upload.wikimedia.org/wikipedia/en/7/77/Utah_Jazz_logo_2025.svg",
  },
  {
    id: "WAS",
    name: "Washington Wizards",
    image:
      "https://upload.wikimedia.org/wikipedia/en/0/02/Washington_Wizards_logo.svg",
  },
];

export const Versus = ({ teams: propTeams = [] }: VersusProps) => {
  const [teamA, setTeamA] = useState("");
  const [teamB, setTeamB] = useState("");
  const [submitted, setSubmitted] = useState(false);
  const [teams, setTeams] = useState<Team[]>(propTeams);
  const [loading, setLoading] = useState(!propTeams.length);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [headToHeadData, setHeadToHeadData] = useState<HeadToHeadData>({});
  const [matchupStats, setMatchupStats] = useState<any>(null);

  // Load teams (API or local)
  useEffect(() => {
    if (propTeams.length > 0) {
      setTeams(propTeams);
      setLoading(false);
      return;
    }

    let timeoutId: number | undefined;
    const fetchTeams = async () => {
      try {
        setLoading(true);
        const controller = new AbortController();
        timeoutId = setTimeout(() => controller.abort(), 3000);

        const response = await fetch(
          "https://matchups.meralus.dev/api/teams-full",
          {
            signal: controller.signal,
          }
        );
        clearTimeout(timeoutId);

        if (!response.ok) throw new Error(`Failed: ${response.status}`);
        const data: Team[] = await response.json();
        setTeams(data);
        setError(null);
        setSuccessMessage("API connection successful");
        setTimeout(() => setSuccessMessage(null), 3000);
      } catch (err: any) {
        console.error(err);
        setTeams(localTeams);
        setError("Failed to load teams from API, using local data.");
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
    return () => clearTimeout(timeoutId);
  }, [propTeams]);

  // Load local head-to-head JSON
  useEffect(() => {
    const loadLocalData = async () => {
      try {
        const res = await fetch(
          `${import.meta.env.BASE_URL}data/headtohead.json`
        );
        if (!res.ok) throw new Error("Failed to load local head-to-head data");
        const json = await res.json();
        setHeadToHeadData(json);
      } catch (err) {
        console.error("Error loading head-to-head data:", err);
        setError("Failed to load head-to-head data");
      }
    };
    loadLocalData();
  }, []);

  const handleSubmit = () => {
    if (teamA && teamB) {
      const matchupKey = `${teamA}_vs_${teamB}`;
      const reverseKey = `${teamB}_vs_${teamA}`;
      const matchup = headToHeadData[matchupKey] || headToHeadData[reverseKey];

      if (!matchup) {
        setError("No data found for this matchup.");
        setMatchupStats(null);
        return;
      }

      setError(null);
      setMatchupStats(matchup);
      setSubmitted(true);
    }
  };

  const handleReset = () => {
    setSubmitted(false);
    setTeamA("");
    setTeamB("");
    setMatchupStats(null);
  };

  const selectedTeams = propTeams.length > 0 ? propTeams : teams;

  return (
    <div id="versus" className="flex flex-col w-full bg-black text-white">
      {/* Messages */}
      {loading && (
        <div className="flex justify-center py-12">
          <p>Loading teams...</p>
        </div>
      )}
      {successMessage && (
        <div className="flex justify-center py-12 text-green-500">
          <p>{successMessage}</p>
        </div>
      )}
      {error && (
        <div className="flex justify-center py-12 text-red-500">
          <p>{error}</p>
        </div>
      )}

      {/* Selectors */}
      {!loading && (
        <div className="flex flex-col items-center py-12 space-y-8">
          <div className="flex flex-row justify-evenly items-center w-full max-w-4xl">
            <CustomSelect
              label="Team A"
              value={teamA}
              onChange={setTeamA}
              options={selectedTeams}
            />
            <h2 className="self-end mx-2 text-lg font-bold">VS</h2>
            <CustomSelect
              label="Team B"
              value={teamB}
              onChange={setTeamB}
              options={selectedTeams}
            />
          </div>

          <div className="flex flex-col items-center space-y-2">
            <button
              onClick={handleSubmit}
              disabled={!teamA || !teamB || loading}
              className={`px-2 py-2 rounded-lg font-semibold transition duration-300 ${
                teamA && teamB && !loading
                  ? "text-white bg-transparent border border-transparent hover:border-white"
                  : "text-gray-light bg-transparent border border-transparent cursor-not-allowed"
              }`}
            >
              Submit
            </button>
            <button
              onClick={handleReset}
              className={`text-sm text-white hover:text-green-400 underline transition-opacity duration-300 ${
                submitted ? "opacity-100 visible" : "opacity-0 invisible"
              }`}
            >
              Reset
            </button>
          </div>
        </div>
      )}

      {/* Matchup Display */}
      <div className="w-full px-4 pb-12">
        <RevealBlock show={submitted && matchupStats && !loading}>
          {matchupStats && matchupStats[teamA] && matchupStats[teamB] ? (
            <>
              <TeamMatchup
                team1={
                  selectedTeams.find((t) => t.short_name === teamA)?.name ||
                  "Team A"
                }
                team2={
                  selectedTeams.find((t) => t.short_name === teamB)?.name ||
                  "Team B"
                }
                team1Image={
                  selectedTeams.find((t) => t.short_name === teamA)?.image ||
                  "/images/default.png"
                }
                team2Image={
                  selectedTeams.find((t) => t.short_name === teamB)?.image ||
                  "/images/default.png"
                }
                record={`${teamA} vs ${teamB}`}
                headToHeadTeam1Stats={matchupStats[teamA]}
                headToHeadTeam2Stats={matchupStats[teamB]}
                statLabels={[]} // unused now
                historicalTeam1Stats={[]}
                historicalTeam2Stats={[]}
                team1Accolades={[]}
                team2Accolades={[]}
              />
              <p className="text-center mt-4 text-gray-400">
                {typeof matchupStats.games_count === "number"
                  ? `Based on ${matchupStats.games_count} games`
                  : "Based on available data"}
              </p>
            </>
          ) : (
            <p className="text-center text-gray-400">
              No head-to-head data found for this matchup.
            </p>
          )}
        </RevealBlock>
      </div>
    </div>
  );
};

export default Versus;
