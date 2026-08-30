package bobguard.modern;

public final class TaxPolicy {
    public double rateFor(String region) {
        return switch (region) {
            case "MX" -> 0.16;
            case "US" -> 0.0825;
            case "EU" -> 0.20;
            default -> throw new IllegalArgumentException("unsupported region");
        };
    }
}
