import { useStore } from "@nanostores/react";
import React from "react";
import { cartItems } from "../stores/cartStore";

export default function CartNavigation() {
  const $cartListItems = useStore(cartItems);

  return (
    <a href="/cart" className="hover:underline hover:cursor-pointer">
      Cart ({Object.values($cartListItems).length})
    </a>
  );
}
