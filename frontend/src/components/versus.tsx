import { useState, useEffect } from "react";
import { TeamMatchup } from "./TeamMatchup";
import { RevealBlock } from "./RevealBlock";
import { CustomSelect } from "./CustomSelect";

interface Team {
  id?: string | number;
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

  // Load teams (API or local JSON fallback)
  useEffect(() => {
    if (propTeams.length > 0) {
      setTeams(propTeams);
      setLoading(false);
      return;
    }

    const fetchTeams = async () => {
      try {
        setLoading(true);

        // Try backend first
        const response = await fetch("http://localhost:5000/api/teams");
        if (!response.ok) throw new Error("API failed");

        const data: Team[] = await response.json();
        setTeams(data);
        setSuccessMessage("Loaded teams from API");
        setError(null);
      } catch (err) {
        console.warn("API failed, loading local JSON...", err);

        // Fallback: load teams from local JSON in public folder
        try {
          const localRes = await fetch(
            `${import.meta.env.BASE_URL}data/localTeams.json`
          );
          if (!localRes.ok) throw new Error("Failed to load localTeams.json");

          const jsonData = await localRes.json();

          // Map JSON fields to Team interface and prepend BASE_URL to logos
          const mappedTeams: Team[] = jsonData.map((t: any) => ({
            id: t.id,
            name: t.name,
            short_name: t.shortName,
            image: `${import.meta.env.BASE_URL}assets/${t.logo}`,
          }));

          setTeams(mappedTeams);
          setError(null);
          setSuccessMessage("Loaded teams from local JSON");
        } catch (jsonErr) {
          console.error(jsonErr);
          setError("Failed to load teams from both API and local JSON.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
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
                statLabels={[]}
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
