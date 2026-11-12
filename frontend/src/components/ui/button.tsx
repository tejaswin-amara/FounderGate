import * as React from "react"

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'default' | 'secondary' | 'outline' | 'ghost' | 'danger'
  size?: 'default' | 'sm' | 'lg' | 'icon'
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => {
    let classes = "inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary disabled:pointer-events-none disabled:opacity-50"

    if (variant === 'default') {
      classes += " bg-primary text-on-primary hover:bg-primary/90"
    } else if (variant === 'secondary') {
      classes += " bg-secondary-container text-on-secondary-container hover:bg-secondary-container/80"
    } else if (variant === 'outline') {
      classes += " border border-outline bg-transparent hover:bg-secondary-container hover:text-on-secondary-container"
    } else if (variant === 'ghost') {
      classes += " hover:bg-secondary-container hover:text-on-secondary-container"
    } else if (variant === 'danger') {
      classes += " bg-error text-on-error hover:bg-error/90"
    }

    if (size === 'default') {
      classes += " h-9 px-4 py-2"
    } else if (size === 'sm') {
      classes += " h-8 rounded-md px-3 text-xs"
    } else if (size === 'lg') {
      classes += " h-10 rounded-md px-8"
    } else if (size === 'icon') {
      classes += " h-9 w-9"
    }

    return (
      <button
        className={`${classes} ${className || ""}`}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button }
