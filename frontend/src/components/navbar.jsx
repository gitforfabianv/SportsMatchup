import { useState } from "react";
import MatchupsLogo from "../assets/MatchupsLogo.svg";
const NAV_LINKS = [
    {
        title: "About",
        link: "https://github.com/gitforfabianv/SportsMatchup/blob/main/README.md",
    },
    {
        title: "Feature Requests",
        link: "https://github.com/gitforfabianv/SportsMatchup/issues",
    },
    { title: "Donate", link: "#donate" },
    { title: "API", link: "/test" },
];
export const Navbar = ({ showApi, setShowApi }) => {
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    return (<div className="w-full sticky top-0 z-50 bg-black shadow-lg shadow-orange-light/50 backdrop-blur-md">
      <div className="h-[65px] flex items-center justify-between px-4">
        {/* Logo */}
        <a href="#about-me" className="flex items-center">
          <img src={MatchupsLogo} alt="Logo" width={70} height={70} draggable={false} className="cursor-pointer m-2"/>
        </a>

        {/* Hamburger Icon */}
        <button onClick={() => setIsMenuOpen((prev) => !prev)} className="text-white hover:text-orange-light transition text-2xl" aria-label="Toggle menu">
          ☰
        </button>
      </div>

      {/* Slide-out Menu */}
      {isMenuOpen && (<div className="absolute right-0 top-[65px] w-64 bg-gray-dark text-white shadow-lg p-4 flex flex-col space-y-4">
          <ul className="flex flex-col items-end space-y-2">
            {NAV_LINKS.map((link) => link.title === "API" ? (<li key={link.title}>
                  <button onClick={() => {
                    setShowApi((prev) => !prev);
                    setIsMenuOpen(false);
                }} className="hover:text-orange-light transition">
                    {showApi ? "Hide API" : "Show API"}
                  </button>
                </li>) : (<li key={link.title}>
                  <a href={link.link} className="hover:text-orange-light transition" onClick={() => setIsMenuOpen(false)}>
                    {link.title}
                  </a>
                </li>))}
          </ul>
        </div>)}
    </div>);
};
