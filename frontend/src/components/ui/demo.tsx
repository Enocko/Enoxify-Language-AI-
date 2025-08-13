import { Scene } from "./rubiks-cube";

const DemoOne = () => {
  return (
    <div className="h-screen w-screen relative flex flex-col justify-center items-center">
      <div className="absolute inset-0">
        <Scene />
      </div>
    </div>
  );
};

export { DemoOne }; 