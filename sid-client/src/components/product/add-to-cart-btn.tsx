import { useStore } from "@nanostores/react";
import { addCartItem, cartItems } from "../../stores/cartStore";
import MdiCartPlus from "../icons/MdiCartPlus";

interface AddToCartBtnProps {
  name: string;
  image: string;
  id: number;
  stock: number;
  price: number;
}

export default function AddToCartBtn({
  name,
  image,
  id,
  stock,
  price,
}: AddToCartBtnProps) {
  return (
    <button
      onClick={(e) => {
        e.preventDefault();
        console.log("add product to cart");
        const product_to_cart = {
          name,
          image,
          price,
          stock,
          id: String(id),
        };
        addCartItem(product_to_cart);
      }}
      className="border bg-gray-800 bg-opacity-50 rounded-lg px-3 py-2 m-3"
    >
      <MdiCartPlus className="w-6 h-6 text-emerald-400" />
    </button>
  );
}
