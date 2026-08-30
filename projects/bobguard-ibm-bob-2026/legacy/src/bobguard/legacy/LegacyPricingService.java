package bobguard.legacy;

public final class LegacyPricingService {
    public double quote(String customerTier, double unitPrice, int quantity, String coupon, String region) {
        if (unitPrice < 0) throw new IllegalArgumentException("unitPrice must be >= 0");
        if (quantity <= 0) throw new IllegalArgumentException("quantity must be > 0");
        if (customerTier == null || region == null) throw new IllegalArgumentException("tier and region are required");

        double subtotal = unitPrice * quantity;
        double discount = 0.0;

        if ("GOLD".equals(customerTier)) {
            discount += subtotal * 0.10;
        } else if ("SILVER".equals(customerTier)) {
            discount += subtotal * 0.05;
        }

        if (quantity >= 20) {
            discount += subtotal * 0.03;
        }

        if (coupon != null && !coupon.isBlank()) {
            if ("SAVE5".equals(coupon)) {
                discount += 5.0;
            } else if ("SAVE10".equals(coupon)) {
                discount += 10.0;
            } else {
                throw new IllegalArgumentException("unknown coupon");
            }
        }

        double discounted = Math.max(0.0, subtotal - discount);
        double taxRate;
        if ("MX".equals(region)) {
            taxRate = 0.16;
        } else if ("US".equals(region)) {
            taxRate = 0.0825;
        } else if ("EU".equals(region)) {
            taxRate = 0.20;
        } else {
            throw new IllegalArgumentException("unsupported region");
        }

        return round2(discounted * (1.0 + taxRate));
    }

    private static double round2(double value) {
        return Math.round(value * 100.0) / 100.0;
    }
}
