import { type NextPage } from "next";
import Head from "next/head";
import { SignUp, useUser } from "@clerk/nextjs";

import { api } from "~/utils/api";

import { useClerk } from "@clerk/clerk-react";

const SignOutButton = () => {
  const { signOut } = useClerk();
  return (
    <button
      className="border-2 border-blue-500 hover:border-red-500 bg-transparent text-blue-600 hover:text-red-600 py-2 px-4 font-semibold rounded"
      onClick={() => signOut()}
    >
      Sign out
    </button>
  );
};

const Home: NextPage = () => {
  const user = useUser();
  const { data } = api.post.getAll.useQuery();

  return (
    <>
      <Head>
        <title>JW Admin</title>
        <meta name="description" content="JW Admin" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className="flex min-h-screen flex-col items-center justify-center bg-gradient-to-b from-[#2e026d] to-[#15162c]">
        {user.isSignedIn
          ?
          <div>
            <SignOutButton />
            {data?.map(post => (
              <div key={post.id}>{post.content}</div>
            ))}
          </div>
          :
          <SignUp />
        }
      </main>
    </>
  );
};

export default Home;
