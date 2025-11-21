type Props = {
  href?: string;
  children?: React.ReactNode;
};

export default function ({ href, children }: Props) {
  return (
    <a className={`p-3 text-sm`} href={href}>
      {children}
    </a>
  );
}
