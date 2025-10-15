export const TeamSelect = ({ label, value, onChange, options, }) => {
    return (<div className="flex flex-col items-start space-y-2">
      <label className="text-sm font-semibold">{label}</label>
      <select value={value} onChange={(e) => onChange(e.target.value)} className="bg-gray-dark text-white px-4 py-2 rounded-lg">
        <option value="">Select a team</option>
        {options.map((team) => (<option key={team.id} value={team.id}>
            {team.name}
          </option>))}
      </select>
    </div>);
};
