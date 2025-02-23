import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '2rem' }}>
      <h1>Welcome to Slash</h1>
      <Link href="/login">
        Go to Login
      </Link>
    </div>
  );
} 