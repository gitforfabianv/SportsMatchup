"use client";
import React from "react";
export const RevealBlock = ({ show, children }) => (<div className="w-full flex justify-center items-center transition-all duration-500">
    <div className={`w-full max-w-4xl bg-black p-6 transform transition-opacity duration-500 ${show
        ? "opacity-100 scale-100"
        : "opacity-0 scale-95 pointer-events-none"}`}>
      {children}
    </div>
  </div>);
