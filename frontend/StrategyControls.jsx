import React, { useState } from 'react';

export default function StrategyControls() {
  const [nlpEnabled, setNlpEnabled] = useState(true);
  const [shadowEnabled, setShadowEnabled] = useState(true);
  const [hftEnabled, setHftEnabled] = useState(false);

  const toggle = (type) => {
    const stateMap = {
      nlp: [nlpEnabled, setNlpEnabled],
      shadow: [shadowEnabled, setShadowEnabled],
      hft: [hftEnabled, setHftEnabled],
    };
    const [val, setter] = stateMap[type];
    setter(!val);
  };

  return (
    <div className="p-4 border rounded bg-white shadow">
      <h2 className="text-lg font-bold mb-2">⚙️ Strategy Control Panel</h2>
      <div>
        <label><input type="checkbox" checked={nlpEnabled} onChange={() => toggle('nlp')} /> NLP Engine</label>
      </div>
      <div>
        <label><input type="checkbox" checked={shadowEnabled} onChange={() => toggle('shadow')} /> Shadow Engine</label>
      </div>
      <div>
        <label><input type="checkbox" checked={hftEnabled} onChange={() => toggle('hft')} /> HFT Engine</label>
      </div>
    </div>
  );
}