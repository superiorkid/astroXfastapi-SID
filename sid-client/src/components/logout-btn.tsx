import React from "react";
import { cookies } from "../lib/cookies";

export default function LogoutButton() {
  return (
    <button
      onClick={() => {
        cookies.remove("access_token");
        cookies.remove("isLoggedin");
        cookies.remove("token_type");
        window.location.reload();
      }}
    >
      Logout
    </button>
  );
}
