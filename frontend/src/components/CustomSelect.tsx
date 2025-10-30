import { useState, useRef, useEffect } from "react";

interface Team {
  id?: string | number;
  name: string;
  image: string;
  short_name?: string;
}

interface CustomSelectProps {
  label: string;
  value: string;
  onChange: (val: string) => void;
  options: Team[];
}

export const CustomSelect = ({
  label,
  value,
  onChange,
  options,
}: CustomSelectProps) => {
  const [open, setOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(e.target as Node)
      ) {
        setOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selected = options.find((opt) => opt.short_name === value);

  return (
    <div
      ref={dropdownRef}
      className="flex flex-col items-start space-y-2 relative w-52 mx-2"
    >
      <label className="text-sm font-semibold text-white">{label}</label>

      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="w-full bg-black text-white py-2 px-6 border border-white flex justify-center items-center"
      >
        {selected ? (
          <div className="flex items-center justify-center space-x-2">
            <img
              src={selected.image}
              alt={selected.name}
              className="h-6 w-6 object-contain"
            />
            <span className="text-left">{selected.name}</span>
          </div>
        ) : (
          <span className="text-gray-400 w-full text-center">
            Select a team
          </span>
        )}
        <span className="ml-2">▾</span>
      </button>

      {open && (
        <div className="absolute top-full left-0 w-full bg-black border border-white mt-1 z-10 max-h-64 overflow-y-auto">
          {options.map((opt, index) => (
            <div
              key={opt.id ?? opt.short_name ?? index} // unique key
              onClick={() => {
                if (opt.short_name) {
                  onChange(opt.short_name);
                  setOpen(false);
                }
              }}
              className={`flex justify-start items-center space-x-2 py-2 pl-2 cursor-pointer hover:bg-gray-700 ${
                value === opt.short_name ? "bg-gray-800" : ""
              }`}
            >
              <img
                src={opt.image}
                alt={opt.name}
                className="h-6 w-6 object-contain"
              />
              <span className="text-center">{opt.name}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
