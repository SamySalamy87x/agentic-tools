package bobguard.modern;

public final class DiscountPolicy {
    public double discount(String customerTier, double subtotal, int quantity, String coupon) {
        double discount = tierDiscount(customerTier, subtotal) + volumeDiscount(subtotal, quantity);
        discount += couponDiscount(coupon);
        return Math.min(subtotal, discount);
    }

    private double tierDiscount(String tier, double subtotal) {
        return switch (tier) {
            case "GOLD" -> subtotal * 0.10;
            case "SILVER" -> subtotal * 0.05;
            default -> 0.0;
        };
    }

    private double volumeDiscount(double subtotal, int quantity) {
        return quantity >= 20 ? subtotal * 0.03 : 0.0;
    }

    private double couponDiscount(String coupon) {
        if (coupon == null || coupon.isBlank()) return 0.0;
        return switch (coupon) {
            case "SAVE5" -> 5.0;
            case "SAVE10" -> 10.0;
            default -> throw new IllegalArgumentException("unknown coupon");
        };
    }
}
