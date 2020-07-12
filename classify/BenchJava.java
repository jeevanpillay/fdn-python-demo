import static java.lang.Math.sin;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Locale;
import java.util.Random;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class BenchJava {

	public static void main(String[] args) {

		final int numTrials = 10;
		final int numPoints = (args.length == 1) ? Integer.parseInt(args[0]) : 500000;
		final long seed = 3247520923L;

		// Generate datasets.
		System.out.println("Initializing dataset of " + numPoints);
		List<List<GaussPoint>> allPoints = new ArrayList<>();
		double[][] allPointsFlat = new double[numTrials][];
		for (int i = 0; i < numTrials; i++) {
			allPoints.add(generateDataset(numPoints, seed+i));
			allPointsFlat[i] = generateFlatDataset(numPoints, seed+i);
		}
		System.out.println("Benchmarking...");
		System.out.println();

		// Plain stream.
		for (List<GaussPoint> points : allPoints) {

			// Time and test.
			long start = System.nanoTime();
			List<Double> scores = points.stream()
										.map(GaussPoint::classify)
										.collect(Collectors.toList());
			double checksum = scores.stream().mapToDouble(Double::valueOf).sum();
			long end = System.nanoTime();

			// Compute reporting quantities.
			double time_us = ((end - start) / 1000D);
			String head = scores.subList(0, 5).stream().map(d -> String.format(Locale.UK, "%5.2f", d)).collect(Collectors.joining(","));
	
			System.out.println(String.format(Locale.UK, "%-12s%9.2fus, checksum %f, head [%s, ...]", "Stream", time_us, checksum, head));
		}

		// Separate.
		System.out.println();

		// C-like in-place.
		for (double[] points : allPointsFlat) {

			// Time and test.
			long start = System.nanoTime();
			double[] scores = inplaceLoop(points);
			double checksum = Arrays.stream(scores).limit(numPoints).sum();
			long end = System.nanoTime();

			// Compute reporting quantities.
			double time_us = ((end - start) / 1000D);
			String head = Arrays.stream(scores).limit(5).mapToObj(d -> String.format(Locale.UK, "%5.2f", d)).collect(Collectors.joining(","));
	
			System.out.println(String.format(Locale.UK, "%-12s%9.2fus, checksum %f, head [%s, ...]", "Loop", time_us, checksum, head));
		}
	}

	private static List<GaussPoint> generateDataset(int numPoints, long seed) {
		final Random rng = new Random(seed);

		return IntStream.range(0, numPoints)
						.mapToObj(i -> new GaussPoint(rng))
						.collect(Collectors.toList());
	}

	private static double[] generateFlatDataset(int numPoints, long seed) {
		final Random rng = new Random(seed);

		return IntStream.range(0, 2*numPoints)
						.mapToDouble(i -> rng.nextGaussian())
						.toArray();
	}

	private static double[] inplaceLoop(final double[] dataset) {
		for (int i = 0; i < dataset.length >> 1; i++) {
			dataset[i] = BenchJava.classify(dataset[i << 1], dataset[(i << 1) + 1]);
		}
		return dataset;
	}

	private static class GaussPoint {

		private final double x;
		private final double y;

		public GaussPoint(Random rng) {
			this.x = rng.nextGaussian();
			this.y = rng.nextGaussian();
		}

		public double classify() {
			return BenchJava.classify(x, y);
		}
	}

	private static double classify(final double x, final double y) {
		double result = Double.NaN;

		if (x > 0.5*y && y < 0.3) {
			result = sin(x - y);
		} else if (x<0.5*y) {
			result = 0;
		} else if (x>0.2*y) {
			result = (2*sin(x+2*y));
		} else {
			result = (sin(y+x));
		}

		return result;
	}
}
