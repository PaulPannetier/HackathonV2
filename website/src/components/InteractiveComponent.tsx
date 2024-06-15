import React, { HTMLAttributes, useRef, useState } from "react";
import SVGMap from "./SVGMap";

interface PopOverProps extends Omit<HTMLAttributes<HTMLDivElement>, "title"> {
  title: React.ReactNode;
}

const PopOver = ({ title, ...props }: PopOverProps) => {
  return <div {...props}>{title}</div>;
};

export const InteractiveMap = () => {
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);
  const [focussedRegion, setFocussedRegion] = useState<string | null>(null);
  const [focusPoint, setFocusPoint] = useState<{ x: number; y: number } | null>(
    null
  );
  const [hoverPos, setHoverPos] = useState<{ x: number; y: number } | null>(
    null
  );
  const [transitioning, setTransitioning] = useState<boolean>(false);
  const outerRef = useRef<HTMLDivElement>(null);
  // console.log(hoverPos);

  console.log(transitioning);
  return (
    <div
      ref={outerRef}
      style={{
        width: "100%",
        aspectRatio: "4/3",
        // overflow: "auto",
        position: "relative",
        padding: "2rem",
        boxSizing: "border-box",
        overflow: transitioning ? "visible" : "hidden"
      }}
    >
      <SVGMap
        onTransitionEnd={({ propertyName }) => {
          if (
            propertyName === "transform" ||
            propertyName === "transform-origin"
          ) {
            setTransitioning(false);
          }
        }}
        style={{
          display: "block",
          objectFit: "cover",
          height: "100%",
          width: "100%",
          transition:
            "fill 325ms ease, transform-origin 300ms linear, transform 425ms ease",
          transformBox: "view-box",
          transformOrigin: "50% 50%",
          transform: "scale(1)",
          overflow: transitioning ? "visible" : "hidden",
          ...(focusPoint
            ? {
                transform: "scale(4)",
                transformOrigin: `calc(0% + ${focusPoint.x}px) calc(0% + ${focusPoint.y}px)`
              }
            : {})
        }}
        highlighedRegions={{
          ...(hoveredRegion
            ? {
                [hoveredRegion]: true
              }
            : {}),
          ...(focussedRegion
            ? {
                [focussedRegion]: true
              }
            : {})
        }}
        onRegionClick={(data) => {
          if ("title" in data && data.title !== focussedRegion) {
            const bcr = (data.event.target as SVGPathElement).getBBox();

            const x = bcr.x + bcr.width / 2;
            const y = bcr.y;

            setFocusPoint({
              x,
              y
            });
            setFocussedRegion(data.title);
            setTransitioning(true);
          } else {
            setFocusPoint(null);
            setFocussedRegion(null);
            setTransitioning(true);
          }
          // console.log(data.event);
        }}
        onRegionMouseOver={(data) => {
          if ("title" in data) {
            setHoveredRegion(data.title);
            // console.log(data.event);
            setHoverPos({
              x: data.event.clientX,
              y: data.event.clientY
            });
          } else if (!("title" in data)) {
            setHoveredRegion(null);
            setHoverPos(null);
          }
          // console.log(data.event);
        }}
      />
      {!transitioning && (
        <PopOver
          title={<div>{hoveredRegion}</div>}
          style={{
            userSelect: "none",
            display: hoverPos ? "block" : "none",
            pointerEvents: "none",
            position: "absolute",
            opacity: hoveredRegion && hoverPos ? 1 : 0,
            top: "0%",
            left: "0%",
            minWidth: "8rem",
            padding: ".375rem .5rem",
            borderRadius: ".375rem",
            lineHeight: 1.5,
            backgroundColor: "white",
            transform: `
            translate(${hoverPos ? hoverPos.x : undefined}px, calc(-50% + ${
              hoverPos ? hoverPos.y + 8 : undefined
            }px))
          `,
            boxShadow: "2px 1px 2px rgba(18, 18, 18, .125)"
          }}
        />
      )}
    </div>
  );
};

export default InteractiveMap;
