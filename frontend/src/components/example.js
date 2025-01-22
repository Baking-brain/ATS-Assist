import React from "react";
import "../static/example.css";

export default function Example(props) {
  const { name } = props;

  return <h3>Example Component: {name}</h3>;
}
