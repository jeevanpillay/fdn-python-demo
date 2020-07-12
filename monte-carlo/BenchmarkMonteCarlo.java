import java.util.Locale;
import java.util.Random;

public class BenchmarkMonteCarlo {

	// Fixed constants.
	private static final int DELTA = 5 * 60;
	private static final int HORIZON = (24 * 60 * 60) / DELTA;
	private static final double T_OUT = 0;

	private static double doRollout(FirstOrderModel tcl, double tStart, int[] schedule) {

		double tIn = tStart;
		double reward = tcl.comfortScore(tIn);

		for (int time = 0; time < HORIZON; time++) {
			tIn = tcl.nextTemperature(tIn, T_OUT, DELTA, schedule[time]);
			reward += tcl.comfortScore(tIn);
		}

		return reward;
	}

	public static void main(String[] args) {

		// Number of simulations to perform.
		final long seed = 74329834795L;
		final int numSimulations = 10000;

		// Create TCL.
		final FirstOrderModel tcl = new FirstOrderModel(20*60, 35*60);

		// Create random number generator.
		final Random rng = new Random(seed);

		double checksum = 0;
		long runtime = 0;
		long fulltime = -System.nanoTime();
		for (int i = 0; i < numSimulations; i++) {
			
			// Create random activation schedule (50% on, 50% off), initial temperature uniform in (18, 20)
			int[] power = rng.doubles().limit(HORIZON).mapToInt(d -> (d < 0.5) ? 0 : 1).toArray();
			double tIn = 18 + 2 * rng.nextDouble();

			runtime -= System.nanoTime();
			checksum += doRollout(tcl, tIn, power);
			runtime += System.nanoTime();
		}
		fulltime = fulltime + System.nanoTime();

		System.out.println(String.format(Locale.UK, "%-12s: per-run %.10fs, total %8.5fs. (checksum %f)", "Java OO", (1e-9) * runtime / numSimulations, (1e-9) * fulltime, checksum));
	}
}
