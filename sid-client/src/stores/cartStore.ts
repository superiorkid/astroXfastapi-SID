import { map } from "nanostores";

export type CartItem = {
  id: string;
  name: string;
  image: string;
  quantity: number;
  price: number;
  stock: number;
};

type ItemDisplayInfo = Pick<
  CartItem,
  "id" | "name" | "image" | "price" | "stock"
>;

export const cartItems = map<Record<string, CartItem>>({});

export function addCartItem({
  id,
  name,
  image,
  price,
  stock,
}: ItemDisplayInfo) {
  const existingEntry = cartItems.get()[id];
  if (existingEntry) {
    cartItems.setKey(id, {
      ...existingEntry,
      quantity: existingEntry.quantity + 1,
      price: existingEntry.price + price,
    });
  } else {
    cartItems.setKey(id, { id, name, image, price, stock, quantity: 1 });
  }
}
