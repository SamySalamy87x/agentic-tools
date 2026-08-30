package bobguard.tests;

import bobguard.legacy.LegacyPricingService;
import bobguard.modern.ModernPricingService;

import java.util.ArrayList;
import java.util.List;

public final class ParityHarness {
    record Case(String tier, double unitPrice, int quantity, String coupon, String region) {}

    public static void main(String[] args) {
        var legacy = new LegacyPricingService();
        var modern = new ModernPricingService();
        var details = new ArrayList<String>();

        List<Case> parity = List.of(
            new Case("STANDARD", 100, 1, null, "MX"),
            new Case("SILVER", 100, 1, null, "MX"),
            new Case("GOLD", 100, 1, null, "MX"),
            new Case("STANDARD", 25, 20, null, "US"),
            new Case("SILVER", 25, 20, "SAVE5", "US"),
            new Case("GOLD", 50, 10, "SAVE10", "EU"),
            new Case("STANDARD", 3.99, 100, "SAVE5", "MX"),
            new Case("GOLD", 1.25, 40, "SAVE10", "US")
        );

        int parityPass = 0;
        for (int i = 0; i < parity.size(); i++) {
            Case c = parity.get(i);
            double a = legacy.quote(c.tier, c.unitPrice, c.quantity, c.coupon, c.region);
            double b = modern.quote(c.tier, c.unitPrice, c.quantity, c.coupon, c.region);
            boolean ok = Double.compare(a, b) == 0;
            if (ok) parityPass++;
            details.add("parity_" + (i + 1) + "=" + (ok ? "PASS" : "FAIL") + " legacy=" + a + " modern=" + b);
        }

        int validationPass = 0;
        boolean quantityFailure = sameFailure(
            () -> legacy.quote("STANDARD", 10, 0, null, "MX"),
            () -> modern.quote("STANDARD", 10, 0, null, "MX")
        );
        if (quantityFailure) validationPass++;
        details.add("validation_quantity=" + (quantityFailure ? "PASS" : "FAIL"));

        boolean couponFailure = sameFailure(
            () -> legacy.quote("STANDARD", 10, 1, "BAD", "MX"),
            () -> modern.quote("STANDARD", 10, 1, "BAD", "MX")
        );
        if (couponFailure) validationPass++;
        details.add("validation_coupon=" + (couponFailure ? "PASS" : "FAIL"));

        boolean pass = parityPass == parity.size() && validationPass == 2;
        System.out.println((pass ? "PASS" : "FAIL") + " parity_cases=" + parityPass + " validation_cases=" + validationPass);
        System.out.println("Behavioral parity: " + (pass ? "PASS" : "FAIL"));
        details.forEach(System.out::println);
        if (!pass) System.exit(1);
    }

    private static boolean sameFailure(Runnable a, Runnable b) {
        Class<?> aType = failureType(a);
        Class<?> bType = failureType(b);
        return aType != null && aType.equals(bType);
    }

    private static Class<?> failureType(Runnable r) {
        try {
            r.run();
            return null;
        } catch (RuntimeException ex) {
            return ex.getClass();
        }
    }
}
