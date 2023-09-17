import React from "react";
import { useRef } from "react";
import { Fireworks } from "@fireworks-js/react";
import type { FireworksHandlers } from "@fireworks-js/react";

export default function FireWorks() {
  const ref = useRef<FireworksHandlers>(null);

  const toggle = () => {
    if (!ref.current) return;
    if (ref.current.isRunning) {
      ref.current.stop();
    } else {
      ref.current.start();
    }
  };

  return (
    <main className="flex justify-center h-[100dvh] items-center">
      <h1 className="text-3xl font-semibold text-gray-700">
        Checkout not implemented yet.
      </h1>
      {/* <div>
        <button onClick={() => toggle()}>Toggle</button>
        <button onClick={() => ref.current!.clear()}>Clear</button>
      </div> */}
      <Fireworks
        ref={ref}
        options={{ opacity: 0.5 }}
        style={{
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          position: "fixed",
        }}
      />
    </main>
  );
}
