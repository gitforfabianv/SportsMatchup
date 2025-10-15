"use client";
import { SOCIALS } from "../constants";
export const Footer = () => {
    return (<div className="w-full bg-transparent text-gray-200 shadow-inner">
      <div className="p-4">
        <div className="w-full flex flex-col items-center justify-center">
          <div className="w-full flex flex-row items-center justify-around flex-wrap">
            <div className="hidden md:flex flex-row gap-5"></div>
          </div>

          <div className="text-[15px] text-center text-gray-400">
            &copy; Ted and Fabian {new Date().getFullYear()} Inc. All rights
            reserved.
          </div>
          <div className="mt-2 flex gap-4 items-center">
            {SOCIALS.map(({ name, icon: Icon, link }) => (<a key={name} href={link} target="_blank" rel="noopener noreferrer" className="text-white hover:text-orange-light transition" aria-label={name}>
                <Icon size={22}/>
              </a>))}
          </div>
        </div>
      </div>
    </div>);
};
