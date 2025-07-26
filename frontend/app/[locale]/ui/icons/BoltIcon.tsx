import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBolt } from '@fortawesome/free-solid-svg-icons';

type BoltIconProps = {
  color?: string;
  fontSize?: string;
};

export default function BoltIcon({ color = 'pink-3', fontSize = '40px' }: BoltIconProps) {
  return (
    <span style={{ fontSize: fontSize }} className={`rotate-[-18deg] text-${color}`} aria-hidden="true">
      <FontAwesomeIcon icon={faBolt} />
    </span>
  );
}
