/**
 * The first-order temperature model defines the temperature inertia characteristics of
 * a specific Thermostatically Controlled Load (TCL) model.
 * 
 * @author Frits de Nijs
 */
public class FirstOrderModel {

	private static final double SETPOINT = 20D;
	private static final double DEADBAND = 0.5D;

	private static final double MIN = SETPOINT - DEADBAND;
	private static final double MAX = SETPOINT + DEADBAND;

	private final double C;
	private final double P;

	/**
	 * A first-order model is instantiated by the number of seconds it takes for the
	 * temperature to reach the upper comfort level when heating, or to decay to the
	 * lower comfort level when not heating, under the reference outdoor temperature
	 * of 0 degrees.
	 * 
	 * Changing the duration should be interpreted intuitively as altering the steepness
	 * of the slope of the exponential decay:
	 *
	 *            |  \
	 * 20.5 = MAX | . *.  .  .  .  .
	 *            |    \
	 *            |     \
	 *            |      \
	 * 19.5 = MIN | .  .  *  .  .  .  
	 *            |   cool \
	 *            |         \
	 *    0 = REF | .  .  .  \------
	 *
	 */
	public FirstOrderModel(int secondsToHeat, int secondsToCool) {

		if (secondsToHeat < 1 || secondsToCool < 1)
			throw new IllegalArgumentException("Decay durations must be strictly positive.");

		final double alpha = computeAlpha(secondsToCool);

		C = computeCapacitance(alpha);
		P = computePower(alpha, secondsToHeat);
	}

	private double computeAlpha(double time) {
		return Math.pow(MIN / MAX, 1D / time);
	}

	private double computeCapacitance(double alpha) {
		return (-1D / 3600D) / Math.log(alpha);
	}

	private double computePower(double alpha, double time) {
		return (MIN * Math.pow(alpha, time) - MAX) / (Math.pow(alpha, time) - 1D);
	}

	public double getResistance() {
		return 1D;
	}

	public double getCapacitance() {
		return C;
	}

	public double getPower() {
		return P;
	}

	public double nextTemperature(double tIn, double tOut, int delta, double power) {

		final double alpha = Math.exp((-delta / 3600D) / C);

		return alpha * tIn + (1-alpha) * (tOut + power * P);
	}

	public double comfortScore(double tIn) {

		double error = Math.max(0, Math.abs(tIn - SETPOINT) - DEADBAND);

		return -error * error;
	}

	@Override
	public String toString() {
		return String.format("<C=%.2f, P=%.2f>", getCapacitance(), getPower());
	}

	@Override
	public int hashCode() {
		return 31 * Double.hashCode(getCapacitance()) + Double.hashCode(getPower());
	}

	@Override
	public boolean equals(Object other) {

		boolean equal = false;

		if (other instanceof FirstOrderModel) {
			equal = deepEquals((FirstOrderModel) other);
		}

		return equal;
	}

	private boolean deepEquals(FirstOrderModel that) {

		boolean equal = true;

		equal = equal && (this.getCapacitance() == that.getCapacitance());
		equal = equal && (this.getPower() == that.getPower());

		return equal;
	}
}
