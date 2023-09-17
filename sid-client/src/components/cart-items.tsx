import React from "react";
import { useStore } from "@nanostores/react";
import { cartItems } from "../stores/cartStore";

export default function CartItems() {
  const $cartListItems = useStore(cartItems);

  return (
    <div>
      {Object.values($cartListItems).length ? (
        <React.Fragment>
          <ul className="space-y-5">
            {Object.values($cartListItems).map((cartItem, index) => (
              <li className="flex space-x-5 border" key={index}>
                <img
                  src={`http://localhost:8001/img/product/${cartItem.image}`}
                  alt={cartItem.name}
                  loading="lazy"
                  className="object-contain w-[200px] h-[250px]"
                />
                <div className="p-5 space-y-2">
                  <h3 className="text-2xl font-bold capitalize">
                    {cartItem.name}
                  </h3>
                  <strong className="text-sm underline">
                    Rp.{cartItem.price}
                  </strong>
                  <p className="font-light">Quantity: {cartItem.quantity}</p>
                </div>
              </li>
            ))}
          </ul>
          <button
            onClick={() => window.location.replace("/checkout")}
            className="border p-2 w-full my-5 font-semibold hover:bg-emerald-400 rounded-md hover:text-white"
          >
            Checkout
          </button>
        </React.Fragment>
      ) : (
        <p>Your cart is empty</p>
      )}
    </div>
  );
}
