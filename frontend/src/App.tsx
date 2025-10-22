import { useEffect, useState } from "react";
import "./App.css";
import { Navbar } from "./components/navbar.tsx";
import Versus from "./components/versus.tsx";
import { Footer } from "./components/footer.tsx";

function App() {
  const [showApi, setShowApi] = useState(false);
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        const res = await fetch("http://backend:5000/api/teams");
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        const data = await res.json();
        console.log("Fetched teams:", data);
        setTeams(data);
      } catch (err: unknown) {
        if (err instanceof Error) {
          console.log(err.message); // Safe to access Error properties
        } else {
          console.log("Unknown error:", err);
        }
      }
    };

    const retryFetch = async (retries = 3, delay = 1000) => {
      for (let i = 0; i < retries; i++) {
        try {
          await fetchTeams();
          break;
        } catch (err) {
          if (i < retries - 1)
            await new Promise((res) => setTimeout(res, delay));
          else throw err;
        }
      }
    };

    retryFetch();
  }, []);

  return (
    <div className="w-full min-h-screen flex flex-col bg-black">
      <Navbar showApi={showApi} setShowApi={setShowApi} />

      <div className="overflow-y-auto">
        <Versus teams={teams} />
        <Footer />
      </div>
    </div>
  );
}

export default App;
