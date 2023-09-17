interface IBlog {
  id: number;
  user_id: number;
  content: string;
  title: string;
  slug: string;
  image: string;
  publication_date: string;
  last_modified: string;
}

interface IUser {
  id: number;
  username: string;
  email: string;
  password: string;
  created_at: string;
  updated_at: string;
}

interface IProduct {
  slug: string;
  name: string;
  id: number;
  image: string;
  created_at: string;
  user_id: number;
  price: number;
  stock: number;
  description: string;
  updated_at: string;
}
