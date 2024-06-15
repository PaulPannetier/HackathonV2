import "./styles.css";
import InteractiveMap from "./components/InteractiveMap";

console.clear();

export default function App() {
  return (
    <div className="App" style={{ overflow: "auto" }}>
      <InteractiveMap />
    </div>
  );
}
