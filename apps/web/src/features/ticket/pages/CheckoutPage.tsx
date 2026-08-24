import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useCheckout } from '../hooks/use-checkout';
import { CheckoutEventSummary } from '../components/checkout/CheckoutEventSummary';
import { CheckoutPaymentMethod } from '../components/checkout/CheckoutPaymentMethod';
import { PixPaymentModal } from '../components/checkout/PixPaymentModal';
import { CheckoutSuccess } from '../components/checkout/CheckoutSuccess';

export function CheckoutPage() {
  const {
    event,
    isLoadingEvent,
    quantity,
    paymentMethod,
    setPaymentMethod,
    errorMessage,
    paymentToken,
    isPixModalOpen,
    setIsPixModalOpen,
    isSuccess,
    isPending,
    handleFinishPurchase,
    navigate,
  } = useCheckout();

  if (isLoadingEvent && !event) {
    return (
      <div className="max-w-2xl mx-auto py-20 text-center font-bold text-foreground-muted">
        Carregando informações do checkout...
      </div>
    );
  }

  if (!event) {
    return (
      <div className="max-w-md mx-auto text-center py-20 space-y-4 px-4">
        <h2 className="text-xl font-black text-foreground">Evento não encontrado</h2>
        <Link
          to="/"
          className="inline-flex items-center gap-2 bg-primary text-white font-bold text-xs px-4 py-2 rounded-full"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Voltar ao início</span>
        </Link>
      </div>
    );
  }

  if (isSuccess) {
    return <CheckoutSuccess />;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-6 space-y-6">
      <button
        onClick={() => navigate(-1)}
        className="inline-flex items-center gap-2 text-xs font-bold text-foreground-muted hover:text-foreground transition cursor-pointer"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Voltar ao evento</span>
      </button>

      <h1 className="text-2xl font-black text-foreground">Checkout</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        <CheckoutEventSummary event={event} quantity={quantity} />

        <CheckoutPaymentMethod
          selectedMethod={paymentMethod}
          onSelectMethod={setPaymentMethod}
          onSubmit={handleFinishPurchase}
          isPending={isPending}
          errorMessage={errorMessage}
        />
      </div>

      {paymentToken && (
        <PixPaymentModal
          isOpen={isPixModalOpen}
          onClose={() => setIsPixModalOpen(false)}
          paymentToken={paymentToken}
          onPaidClick={() => {
            setIsPixModalOpen(false);
            navigate('/my-tickets');
          }}
        />
      )}
    </div>
  );
}