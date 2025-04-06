import React from "react";
import { Button } from "@/components/ui/button";

export const StrategyControls = () => {
  const handleStart = async () => {
    await fetch("/api/strategy/start", { method: "POST" });
  };

  const handleStop = async () => {
    await fetch("/api/strategy/stop", { method: "POST" });
  };

  return (
    <div className="p-4 bg-white shadow-xl rounded-2xl">
      <h2 className="text-xl font-semibold mb-2">🚀 Strategy Controls</h2>
      <div className="space-x-2">
        <Button onClick={handleStart}>Start</Button>
        <Button variant="destructive" onClick={handleStop}>Stop</Button>
      </div>
    </div>
  );
};
