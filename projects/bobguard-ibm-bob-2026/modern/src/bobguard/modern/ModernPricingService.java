package bobguard.modern;

public final class ModernPricingService {
    private final DiscountPolicy discountPolicy;
    private final TaxPolicy taxPolicy;

    public ModernPricingService() {
        this(new DiscountPolicy(), new TaxPolicy());
    }

    ModernPricingService(DiscountPolicy discountPolicy, TaxPolicy taxPolicy) {
        this.discountPolicy = discountPolicy;
        this.taxPolicy = taxPolicy;
    }

    public double quote(String customerTier, double unitPrice, int quantity, String coupon, String region) {
        validate(customerTier, unitPrice, quantity, region);
        double subtotal = unitPrice * quantity;
        double discount = discountPolicy.discount(customerTier, subtotal, quantity, coupon);
        double net = subtotal - discount;
        return round2(net * (1.0 + taxPolicy.rateFor(region)));
    }

    private static void validate(String tier, double unitPrice, int quantity, String region) {
        if (unitPrice < 0) throw new IllegalArgumentException("unitPrice must be >= 0");
        if (quantity <= 0) throw new IllegalArgumentException("quantity must be > 0");
        if (tier == null || region == null) throw new IllegalArgumentException("tier and region are required");
    }

    private static double round2(double value) {
        return Math.round(value * 100.0) / 100.0;
    }
}
